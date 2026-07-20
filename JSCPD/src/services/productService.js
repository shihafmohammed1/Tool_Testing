const deps = require('../utils/serviceDeps');
const { stampCreatedAt } = require('../utils/recordBuilder');

const validateProduct = deps.createEntityValidator(['name', 'price']);

function buildProductRecord(payload) {
  const data = validateProduct(payload);
  deps.validatePositiveNumber(data.price, 'price');

  return stampCreatedAt({
    name: data.name.trim(),
    price: data.price,
    category: data.category || 'general',
  });
}

function applyDiscount(product, percentage) {
  deps.validatePositiveNumber(percentage, 'percentage');
  const discounted = product.price * (1 - percentage / 100);

  return {
    ...product,
    price: Number(discounted.toFixed(2)),
    label: deps.formatCurrency(discounted),
  };
}

module.exports = {
  buildProductRecord,
  applyDiscount,
};
