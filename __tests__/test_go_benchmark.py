# Copyright 2026 Zaphiro Technologies
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from pathlib import Path
import subprocess
import tempfile
import types
import unittest

import yaml


WORKFLOW = Path(__file__).resolve().parents[1] / ".github/workflows/golang.yaml"
STEPS = yaml.safe_load(WORKFLOW.read_text())["jobs"]["benchmark"]["steps"]


def step(name):
    return next(item for item in STEPS if item.get("name") == name)


# Test the deployed inline script, not a second copy of the comparator.
SCRIPT = step("Compare benchmark results")["run"]
LINES = SCRIPT.strip().splitlines()
assert LINES[0] == "python3 <<'PY'" and LINES[-1] == "PY"
COMPARATOR = types.ModuleType("go_benchmark")
exec(compile("\n".join(LINES[1:-1]), str(WORKFLOW), "exec"), COMPARATOR.__dict__)


class ComparisonTests(unittest.TestCase):
    def results(self, metrics, name="BenchmarkDecode-2", package="example/stream"):
        return COMPARATOR.parse_results(f"pkg: {package}\n{name} 1000 {metrics}\n")

    def test_go_output_with_packages_and_standard_metrics(self):
        output = """goos: linux
pkg: example/stream
cpu: AMD EPYC 9V45
BenchmarkDecode/size=100-2 1000 2.3e+04 ns/op 221.61 MB/s 496 B/op 9 allocs/op
PASS
pkg: example/core
BenchmarkDecode/size=100-8 1000 42 ns/op
"""
        results = COMPARATOR.parse_results(output)
        self.assertEqual(len(results), 5)
        self.assertEqual(results[("example/stream", "BenchmarkDecode/size=100", "ns/op")], 23000)
        self.assertEqual(results[("example/stream", "BenchmarkDecode/size=100", "MB/s")], 221.61)
        self.assertEqual(results[("example/core", "BenchmarkDecode/size=100", "ns/op")], 42)

    def test_repeated_samples_use_median(self):
        results = COMPARATOR.parse_results(
            "BenchmarkFoo-2 1 100 ns/op\n"
            "BenchmarkFoo-2 1 1000 ns/op\n"
            "BenchmarkFoo-2 1 110 ns/op\n"
        )
        self.assertEqual(results[("", "BenchmarkFoo", "ns/op")], 110)

    def test_invalid_measurements_are_rejected(self):
        for value in ("NaN", "Inf", "-1"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.results(f"{value} ns/op")

    def test_threshold_validation(self):
        self.assertEqual(COMPARATOR.parse_threshold("150%"), 1.5)
        self.assertEqual(COMPARATOR.parse_threshold("100%"), 1)
        for value in ("1.5", "50%", "0%", "NaN%", "Inf%", "abc%"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                COMPARATOR.parse_threshold(value)

    def test_cost_regressions_are_gated_at_existing_threshold(self):
        for unit in ("ns/op", "B/op", "allocs/op"):
            with self.subTest(unit=unit):
                base = self.results(f"100 {unit}")
                _, alerts = COMPARATOR.compare_results(base, self.results(f"150 {unit}"), 1.5)
                self.assertFalse(alerts)
                _, alerts = COMPARATOR.compare_results(base, self.results(f"151 {unit}"), 1.5)
                self.assertEqual(len(alerts), 1)

    def test_storer_throughput_improvement_is_not_a_regression(self):
        base = self.results("790.8 ns/op 103.70 MB/s 496 B/op 9 allocs/op")
        head = self.results("370.0 ns/op 221.61 MB/s 496 B/op 9 allocs/op")
        _, alerts = COMPARATOR.compare_results(base, head, 1.5)
        self.assertFalse(alerts)

    def test_throughput_decrease_is_gated(self):
        rows, alerts = COMPARATOR.compare_results(
            self.results("100 MB/s"), self.results("50 MB/s"), 1.5
        )
        self.assertEqual(rows[0][3], 2)
        self.assertEqual(len(alerts), 1)

    def test_zero_measurements(self):
        for unit in ("ns/op", "MB/s"):
            zero = self.results(f"0 {unit}")
            _, alerts = COMPARATOR.compare_results(zero, zero, 1.5)
            self.assertFalse(alerts)
        _, alerts = COMPARATOR.compare_results(self.results("0 B/op"), self.results("1 B/op"), 1.5)
        self.assertEqual(len(alerts), 1)
        _, alerts = COMPARATOR.compare_results(self.results("1 MB/s"), self.results("0 MB/s"), 1.5)
        self.assertEqual(len(alerts), 1)

    def test_new_or_renamed_benchmarks_have_no_baseline(self):
        rows, alerts = COMPARATOR.compare_results(
            self.results("100 ns/op"), self.results("1000 ns/op", name="BenchmarkNew-2"), 1.5
        )
        self.assertIsNone(rows[0][3])
        self.assertFalse(alerts)

    def run_comparison(self, directory, head, base=None):
        if base is not None:
            (directory / "base.txt").write_text(base)
        (directory / "head.txt").write_text(head)
        return subprocess.run(
            ["bash", "-e", "-o", "pipefail", "-c", SCRIPT],
            env={
                **os.environ,
                "BENCHMARK_RESULTS": str(directory),
                "ALERT_THRESHOLD": "150%",
                "BASE_SHA": "abc123" if base is not None else "",
                "HEAD_SHA": "def456",
                "GITHUB_STEP_SUMMARY": str(directory / "summary.md"),
            },
            capture_output=True, text=True,
        )

    def test_failure_still_writes_summary_and_artifact(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            result = self.run_comparison(
                directory, "BenchmarkFoo-2 100 200 ns/op\n", "BenchmarkFoo-2 100 100 ns/op\n"
            )
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn("::error::", result.stdout)
            report = (directory / "comparison.md").read_text()
            self.assertIn("REGRESSION", report)
            self.assertEqual(report, (directory / "summary.md").read_text())

    def test_first_run_records_results_without_failure(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            result = self.run_comparison(directory, "BenchmarkFoo-2 100 100 ns/op\n")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("::notice::", result.stdout)
            self.assertIn("0 metrics compared; 1 new", (directory / "summary.md").read_text())

    def test_removed_benchmarks_are_visible(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            result = self.run_comparison(directory, "PASS\n", "BenchmarkFoo-2 100 100 ns/op\n")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("1 removed", (directory / "summary.md").read_text())

    def test_artifacts_exclude_unmasked_command_logs(self):
        paths = step("Upload benchmark comparison")["with"]["path"].splitlines()
        self.assertEqual(paths, [
            "${{ env.BENCHMARK_RESULTS }}/comparison.md",
            "${{ env.BENCHMARK_RESULTS }}/environment.txt",
        ])


class WorkflowShellTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.bin = self.directory / "bin"
        self.bin.mkdir()
        self.environment = {
            **os.environ,
            "PATH": str(self.bin) + os.pathsep + os.environ["PATH"],
            "RUNNER_TEMP": str(self.directory),
            "BENCHMARK_RESULTS": str(self.directory / "results"),
            "GITHUB_ENV": str(self.directory / "environment"),
            "GITHUB_OUTPUT": str(self.directory / "outputs"),
            "COMPOSE_PROJECT_NAME": "benchmark-test-1",
            "BASE_SHA": "",
        }
        for command in ("go", "lscpu"):
            self.stub(command, "echo test-environment\n")

    def stub(self, name, body):
        path = self.bin / name
        path.write_text("#!/usr/bin/env bash\nset -eu\n" + body)
        path.chmod(0o755)

    def git(self, *arguments):
        return subprocess.check_output(
            ["git", "-c", "user.name=Benchmark Test", "-c", "user.email=test@example.invalid",
             "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null", *arguments],
            cwd=self.directory, text=True, stderr=subprocess.DEVNULL,
        ).strip()

    def prepare(self, commits=2, explicit_base=False):
        self.git("init", "-b", "main")
        for i in range(commits):
            (self.directory / "value").write_text(str(i))
            self.git("add", "value")
            self.git("commit", "-m", f"Commit {i}")
        if explicit_base:
            self.environment["BASE_SHA"] = self.git("rev-parse", "HEAD^")
        return subprocess.run(
            ["bash", "-e", "-o", "pipefail", "-c", step("Prepare same-runner baseline")["run"]],
            cwd=self.directory, env=self.environment, capture_output=True, text=True,
        )

    def test_base_is_a_separate_worktree_without_changing_candidate(self):
        result = self.prepare(explicit_base=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.directory / "go-benchmark-base/value").read_text(), "0")
        self.assertEqual((self.directory / "value").read_text(), "1")

    def test_manual_run_uses_parent_commit(self):
        result = self.prepare()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(f"sha={self.git('rev-parse', 'HEAD^')}", (self.directory / "outputs").read_text())

    def test_initial_commit_has_no_baseline(self):
        self.environment["BASE_SHA"] = "0" * 40
        result = self.prepare(commits=1)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.directory / "go-benchmark-base").exists())
        self.assertIn("::notice::", result.stdout)

    def test_failed_benchmark_is_not_hidden_by_tee(self):
        (self.directory / "results").mkdir()
        self.stub("make", "echo benchmark-failed >&2\nexit 23\n")
        for name, filename in (("Run baseline benchmark", "base.txt"), ("Run candidate benchmark", "head.txt")):
            with self.subTest(name=name):
                result = subprocess.run(
                    ["bash", "-e", "-o", "pipefail", "-c", step(name)["run"]],
                    env=self.environment, capture_output=True, text=True,
                )
                self.assertEqual(result.returncode, 23)
                self.assertIn("benchmark-failed", (self.directory / "results" / filename).read_text())

    def test_cleanup_only_targets_job_owned_compose_resources(self):
        self.assertEqual(self.prepare().returncode, 0)
        calls = self.directory / "docker-calls"
        self.stub("docker", f"""
        echo "$*" >> '{calls}'
        case "$1" in
          ps) echo test-container ;;
          volume) [[ "$2" != ls ]] || echo test-volume ;;
          network) [[ "$2" != ls ]] || echo test-network ;;
        esac
        """)
        result = subprocess.run(
            ["bash", str(self.directory / "cleanup-go-benchmark.sh")],
            env=self.environment, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(calls.read_text().splitlines(), [
            "ps -aq --filter label=com.docker.compose.project=benchmark-test-1",
            "rm --force --volumes test-container",
            "volume ls -q --filter label=com.docker.compose.project=benchmark-test-1",
            "volume rm test-volume",
            "network ls -q --filter label=com.docker.compose.project=benchmark-test-1",
            "network rm test-network",
        ])


if __name__ == "__main__":
    unittest.main()
