const fs = require('node:fs');
const path = require('node:path');
const { computeGateReport } = require('./metrics-utils');

function buildPlatformJscpdJson(gateReport) {
  const platformScores = gateReport.platformScores;

  return {
    exit: gateReport.all_gates_passed ? 0 : 1,
    scan_ok: true,
    report_path: 'jscpd/0/jscpd_report.json',
    cloneCount: gateReport.cloneCount,
    duplicatedLines: gateReport.duplicatedLines,
    totalLines: gateReport.totalLines,
    DuplicationPercent: gateReport.duplicationPercent,
    MultiPointFailureProbability: platformScores.MultiPointFailureProbability,
    RedundancyLocalization: platformScores.RedundancyLocalization,
    StructuralCleanlinessScore: platformScores.StructuralCleanlinessScore,
    TestSuiteStreamlining: platformScores.TestSuiteStreamlining,
    AbstractionPotential: platformScores.AbstractionPotential,
    RegressionFocusMapping: platformScores.RegressionFocusMapping,
    SynchronizationVerification: platformScores.SynchronizationVerification,
    gate_name: gateReport.gate_name,
    tool: gateReport.tool,
    execution_status: gateReport.execution_status,
    overall_score: gateReport.overallScore,
    all_gates_passed: gateReport.all_gates_passed,
    metrics: gateReport.metrics.map((metric) => ({
      classification: metric.classification,
      value: metric.value,
      execution_status: metric.execution_status,
      result: metric.result,
      coverage: metric.coverage,
    })),
  };
}

function main() {
  const rootDir = process.cwd();
  const gateReport = computeGateReport(rootDir);
  const platformReport = buildPlatformJscpdJson(gateReport);

  const platformDir = path.join(rootDir, 'jscpd', '0');
  fs.mkdirSync(platformDir, { recursive: true });

  const platformFile = path.join(platformDir, 'jscpd.json');
  const gateSummaryFile = path.join(rootDir, 'reports', 'code-duplication-gate.json');
  const metricsReportFile = path.join(rootDir, 'reports', 'metrics-report.json');

  fs.mkdirSync(path.join(rootDir, 'reports'), { recursive: true });
  fs.writeFileSync(platformFile, `${JSON.stringify(platformReport, null, 2)}\n`);
  fs.writeFileSync(gateSummaryFile, `${JSON.stringify(gateReport, null, 2)}\n`);
  fs.writeFileSync(
    metricsReportFile,
    `${JSON.stringify(
      {
        generatedAt: new Date().toISOString(),
        tool: 'jscpd',
        overallScore: `${gateReport.overallScore}/100`,
        overallScoreValue: gateReport.overallScore,
        metrics: gateReport.metrics,
        platformFile: 'jscpd/0/jscpd.json',
      },
      null,
      2
    )}\n`
  );

  console.log(`Overall Score: ${gateReport.overallScore}/100`);
  console.log(`All Gates Passed: ${gateReport.all_gates_passed ? 'YES' : 'NO'}`);
  console.log(`Platform jscpd.json: ${platformFile}`);
  console.log(`Structural Cleanliness: ${platformReport.StructuralCleanlinessScore}/100`);
  console.log(`Test Suite Streamlining: ${platformReport.TestSuiteStreamlining}/100`);

  if (!gateReport.all_gates_passed) {
    process.exit(1);
  }
}

main();
