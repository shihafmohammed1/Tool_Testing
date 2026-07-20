const { validateRequiredFields, validateEmail } = require('./validation');
const { formatDisplayName } = require('./formatting');

function createEntityValidator(requiredFields) {
  return (payload) => {
    validateRequiredFields(payload, requiredFields);
    return payload;
  };
}

function normalizeEntityName(firstName, lastName) {
  return formatDisplayName(firstName, lastName);
}

module.exports = {
  createEntityValidator,
  normalizeEntityName,
  validateEmail,
};
