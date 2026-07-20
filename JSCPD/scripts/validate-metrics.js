const { computeGateReport } = require('./metrics-utils');

function printReport(gateReport) {
  console.log('\n========================================');
  console.log('  JSCPD Code Duplication Metrics Report');
  console.log('========================================\n');

  gateReport.metrics.forEach((metric) => {
    console.log(`Objective : ${metric.classification}`);
    console.log(`Score     : ${metric.score}/100`);
    console.log(`Coverage  : ${metric.coverage}%`);
    console.log(`Result    : ${metric.result}`);
    console.log(`Scope     : ${metric.scanScope.join(', ')}`);
    console.log(`Details   : ${metric.details.duplicationPercentage}% duplicated, ${metric.details.cloneCount} clones`);
    console.log('----------------------------------------');
  });

  console.log(`\nOverall Score: ${gateReport.overallScore}/100`);
  console.log(
    `Status       : ${
      gateReport.overallScore === 100
        ? 'PASS - Ready for trainer validation'
        : 'FAIL - Duplication detected'
    }\n`
  );
}

function main() {
  const gateReport = computeGateReport();
  printReport(gateReport);

  if (gateReport.overallScore < 100) {
    process.exit(1);
  }
}

main();
