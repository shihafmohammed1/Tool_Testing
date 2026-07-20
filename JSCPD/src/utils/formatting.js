function formatDisplayName(firstName, lastName) {
  return `${firstName.trim()} ${lastName.trim()}`;
}

function formatCurrency(amount, currency = 'USD') {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
  }).format(amount);
}

function formatTimestamp(date) {
  return new Date(date).toISOString();
}

module.exports = {
  formatDisplayName,
  formatCurrency,
  formatTimestamp,
};
