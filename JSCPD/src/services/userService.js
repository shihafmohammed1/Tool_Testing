const { createEntityValidator, normalizeEntityName, validateEmail } = require('../utils/entityHelpers');
const { formatTimestamp } = require('../utils/formatting');
const { stampCreatedAt, stampUpdatedAt } = require('../utils/recordBuilder');

const validateUser = createEntityValidator(['firstName', 'lastName', 'email']);

function buildUserRecord(payload) {
  const data = validateUser(payload);
  validateEmail(data.email);

  return stampCreatedAt({
    name: normalizeEntityName(data.firstName, data.lastName),
    email: data.email.toLowerCase(),
    role: data.role || 'member',
  });
}

function updateUserRole(user, nextRole) {
  if (!nextRole) {
    throw new Error('Role is required');
  }

  return stampUpdatedAt(user, { role: nextRole });
}

module.exports = {
  buildUserRecord,
  updateUserRole,
};
