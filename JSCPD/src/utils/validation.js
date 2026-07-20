function validateRequiredFields(payload, fields) {
  const missing = fields.filter((field) => {
    const value = payload[field];
    return value === undefined || value === null || value === '';
  });

  if (missing.length > 0) {
    throw new Error(`Missing required fields: ${missing.join(', ')}`);
  }
}

function validateEmail(email) {
  const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!pattern.test(email)) {
    throw new Error('Invalid email address');
  }
}

function validatePositiveNumber(value, fieldName) {
  if (typeof value !== 'number' || value <= 0) {
    throw new Error(`${fieldName} must be a positive number`);
  }
}

module.exports = {
  validateRequiredFields,
  validateEmail,
  validatePositiveNumber,
};
