const fs = require('node:fs');
const path = require('node:path');

const REQUIRED_CLASSIFICATIONS = [
  'Defect Propagation Risk Detection',
  'Refactoring Identification',
  'Code Quality Assessment',
  'Test Maintenance Reduction',
  'Refactoring Opportunity Detection',
  'Risk-Based Testing Prioritization',
  'Maintainability Testing',
];

const PLATFORM_SCORE_KEYS = [
  'MultiPointFailureProbability',
  'RedundancyLocalization',
  'StructuralCleanlinessScore',
  'TestSuiteStreamlining',
  'AbstractionPotential',
  'RegressionFocusMapping',
  'SynchronizationVerification',
];

function validatePlatformJson(data, requirePerfect = false) {
  const errors = [];

  if (data.exit !== 0) {
    errors.push(`exit must be 0, got ${JSON.stringify(data.exit)}`);
  }
  if (data.scan_ok !== true) {
    errors.push('scan_ok must be true');
  }

  for (const key of PLATFORM_SCORE_KEYS) {
    if (!(key in data)) {
      errors.push(`missing platform score key: ${key}`);
      continue;
    }

    const value = data[key];
    if (typeof value !== 'number') {
      errors.push(`${key} must be numeric, got ${typeof value}`);
      continue;
    }

    if (value <= 1 && key !== 'DuplicationPercent') {
      errors.push(
        `${key}=${value} looks like a 0-1 fraction; TESTABLE expects 0-100 scale`
      );
    }

    const minScore = requirePerfect ? 100 : 70;
    if (value < minScore) {
      errors.push(`${key}=${value} below required minimum ${minScore}`);
    }
  }

  if (!Array.isArray(data.metrics)) {
    errors.push('metrics array missing from platform JSON');
    return errors;
  }

  const byName = Object.fromEntries(
    data.metrics
      .filter((metric) => metric && typeof metric === 'object')
      .map((metric) => [metric.classification, metric])
  );

  for (const name of REQUIRED_CLASSIFICATIONS) {
    if (!(name in byName)) {
      errors.push(`missing classification in metrics[]: ${name}`);
      continue;
    }

    const metric = byName[name];
    const minValue = requirePerfect ? 100 : 70;
    if (metric.result !== 'PASS') {
      errors.push(`${name}: result must be PASS, got ${JSON.stringify(metric.result)}`);
    }
    if (typeof metric.value !== 'number' || metric.value < minValue) {
      errors.push(`${name}: value=${JSON.stringify(metric.value)} below ${minValue}`);
    }
    if (typeof metric.coverage !== 'number' || metric.coverage < minValue) {
      errors.push(`${name}: coverage=${JSON.stringify(metric.coverage)} below ${minValue}`);
    }
  }

  return errors;
}

function main() {
  const requirePerfect = process.argv.includes('--require-100');
  const fileArgIndex = process.argv.indexOf('--file');
  const platformFile =
    fileArgIndex >= 0
      ? path.resolve(process.argv[fileArgIndex + 1])
      : path.join(process.cwd(), 'jscpd', '0', 'jscpd.json');

  if (!fs.existsSync(platformFile)) {
    console.error(`FAIL: platform file not found: ${platformFile}`);
    console.error('Run: node scripts/export_testable_jscpd.js');
    process.exit(2);
  }

  const data = JSON.parse(fs.readFileSync(platformFile, 'utf8'));
  const errors = validatePlatformJson(data, requirePerfect);

  if (errors.length > 0) {
    console.log('METRICS GATE VALIDATION: FAIL');
    errors.forEach((error) => console.log(`  - ${error}`));
    process.exit(1);
  }

  const mode = requirePerfect ? '100/100' : 'gate thresholds';
  console.log(`METRICS GATE VALIDATION: PASS (${mode})`);
  console.log(`  File: ${platformFile}`);
  console.log(`  Structural Cleanliness: ${data.StructuralCleanlinessScore}/100`);
  console.log(`  Test Suite Streamlining: ${data.TestSuiteStreamlining}/100`);
  console.log(`  Classifications: ${REQUIRED_CLASSIFICATIONS.length}/7 PASS`);
}

if (require.main === module) {
  main();
}

module.exports = {
  REQUIRED_CLASSIFICATIONS,
  PLATFORM_SCORE_KEYS,
  validatePlatformJson,
};
