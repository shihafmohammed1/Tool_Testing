const { execSync } = require('node:child_process');
const fs = require('node:fs');
const path = require('node:path');

const GATE_MIN_LINES = 2;
const GATE_MIN_TOKENS = 20;

const CLASSIFICATIONS = [
  {
    classification: 'Defect Propagation Risk Detection',
    secondaryMetric: 'MultiPointFailureProbability',
    scanPaths: ['src', 'tests'],
    weight: 'cloneCount',
  },
  {
    classification: 'Refactoring Identification',
    secondaryMetric: 'RedundancyLocalization',
    scanPaths: ['src', 'tests'],
    weight: 'cloneCount',
  },
  {
    classification: 'Code Quality Assessment',
    secondaryMetric: 'StructuralCleanlinessScore',
    scanPaths: ['src'],
    weight: 'duplicationPercentage',
  },
  {
    classification: 'Test Maintenance Reduction',
    secondaryMetric: 'TestSuiteStreamlining',
    scanPaths: ['tests'],
    weight: 'duplicationPercentage',
  },
  {
    classification: 'Refactoring Opportunity Detection',
    secondaryMetric: 'AbstractionPotential',
    scanPaths: ['src', 'tests'],
    weight: 'cloneCount',
  },
  {
    classification: 'Risk-Based Testing Prioritization',
    secondaryMetric: 'RegressionFocusMapping',
    scanPaths: ['src', 'tests'],
    weight: 'duplicationPercentage',
  },
  {
    classification: 'Maintainability Testing',
    secondaryMetric: 'SynchronizationVerification',
    scanPaths: ['src', 'tests'],
    weight: 'duplicationPercentage',
  },
];

function scoreFromDuplication(percentage) {
  return Math.max(0, Math.round(100 - percentage));
}

function scoreFromClones(cloneCount) {
  return cloneCount === 0 ? 100 : Math.max(0, 100 - cloneCount * 10);
}

function runJscpdScan(scanPaths, outputDir) {
  fs.mkdirSync(outputDir, { recursive: true });

  const args = [
    'npx jscpd',
    scanPaths.join(' '),
    '--config .jscpd.json',
    `--min-lines ${GATE_MIN_LINES}`,
    `--min-tokens ${GATE_MIN_TOKENS}`,
    `--output ${outputDir}`,
  ].join(' ');

  try {
    execSync(args, { stdio: 'pipe', encoding: 'utf8' });
  } catch (error) {
    if (!error.stdout && !error.stderr) {
      throw error;
    }
  }

  const reportPath = path.join(outputDir, 'jscpd-report.json');
  if (!fs.existsSync(reportPath)) {
    throw new Error(`JSCPD report not found at ${reportPath}`);
  }

  return JSON.parse(fs.readFileSync(reportPath, 'utf8'));
}

function buildMetricResult(definition, stats) {
  const score =
    definition.weight === 'cloneCount'
      ? scoreFromClones(stats.clones)
      : scoreFromDuplication(stats.percentage);

  return {
    classification: definition.classification,
    secondaryMetric: definition.secondaryMetric,
    value: score,
    score,
    coverage: score,
    execution_status: 'COMPLETED',
    result: score === 100 ? 'PASS' : 'FAIL',
    scanScope: definition.scanPaths,
    details: {
      duplicatedLines: stats.duplicatedLines,
      totalLines: stats.lines,
      duplicationPercentage: Number(stats.percentage.toFixed(2)),
      cloneCount: stats.clones,
    },
  };
}

function computeGateReport(rootDir = process.cwd()) {
  const tempOutput = path.join(rootDir, 'reports', 'jscpd-scan-temp');
  const metricResults = CLASSIFICATIONS.map((definition) => {
    const report = runJscpdScan(definition.scanPaths, tempOutput);
    return buildMetricResult(definition, report.statistics.total);
  });

  const overallReport = runJscpdScan(['src', 'tests'], tempOutput);
  const overallStats = overallReport.statistics.total;
  const overallScore = Math.round(
    metricResults.reduce((sum, metric) => sum + metric.score, 0) / metricResults.length
  );

  return {
    gate_name: 'Code Duplication Gate',
    tool: 'jscpd',
    execution_status: 'COMPLETED',
    gateSettings: {
      minLines: GATE_MIN_LINES,
      minTokens: GATE_MIN_TOKENS,
    },
    cloneCount: overallStats.clones,
    duplicatedLines: overallStats.duplicatedLines,
    totalLines: overallStats.lines,
    duplicationPercent: Number(overallStats.percentage.toFixed(2)),
    overallScore,
    all_gates_passed: metricResults.every((metric) => metric.result === 'PASS'),
    metrics: metricResults,
    platformScores: Object.fromEntries(
      metricResults.map((metric) => [metric.secondaryMetric, metric.score])
    ),
  };
}

module.exports = {
  CLASSIFICATIONS,
  GATE_MIN_LINES,
  GATE_MIN_TOKENS,
  computeGateReport,
  scoreFromDuplication,
  scoreFromClones,
};
