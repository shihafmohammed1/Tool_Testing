const { formatTimestamp } = require('./formatting');

function createRecordId() {
  return crypto.randomUUID();
}

function stampCreatedAt(fields) {
  return {
    ...fields,
    id: createRecordId(),
    createdAt: formatTimestamp(new Date()),
  };
}

function stampUpdatedAt(record, changes) {
  return {
    ...record,
    ...changes,
    updatedAt: formatTimestamp(new Date()),
  };
}

module.exports = {
  stampCreatedAt,
  stampUpdatedAt,
};
