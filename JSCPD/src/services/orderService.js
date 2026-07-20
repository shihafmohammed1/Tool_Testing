const {
  createEntityValidator,
  validatePositiveNumber,
  formatCurrency,
  formatTimestamp,
} = require('../utils/serviceDeps');
const { stampCreatedAt, stampUpdatedAt } = require('../utils/recordBuilder');

const validateOrder = createEntityValidator(['customerId', 'items']);

function sumLineItems(items) {
  return items.reduce((sum, item) => {
    validatePositiveNumber(item.quantity, 'quantity');
    validatePositiveNumber(item.unitPrice, 'unitPrice');
    return sum + item.quantity * item.unitPrice;
  }, 0);
}

function buildOrderRecord(payload) {
  const data = validateOrder(payload);

  if (!Array.isArray(data.items) || data.items.length === 0) {
    throw new Error('Order must contain at least one item');
  }

  const total = sumLineItems(data.items);

  return stampCreatedAt({
    customerId: data.customerId,
    items: data.items,
    total: Number(total.toFixed(2)),
    totalLabel: formatCurrency(total),
    status: 'pending',
  });
}

function markOrderShipped(order) {
  return stampUpdatedAt(order, {
    status: 'shipped',
    shippedAt: formatTimestamp(new Date()),
  });
}

module.exports = {
  buildOrderRecord,
  markOrderShipped,
};
