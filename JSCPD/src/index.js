const { buildUserRecord, updateUserRole } = require('./services/userService');
const { buildProductRecord, applyDiscount } = require('./services/productService');
const { buildOrderRecord, markOrderShipped } = require('./services/orderService');

function bootstrapDemoData() {
  const admin = buildUserRecord({
    firstName: 'Alex',
    lastName: 'Trainer',
    email: 'alex.trainer@example.com',
    role: 'admin',
  });

  const catalog = [
    buildProductRecord({ name: 'Keyboard', price: 79.99, category: 'hardware' }),
    buildProductRecord({ name: 'Mouse', price: 39.99, category: 'hardware' }),
  ].map((product) => applyDiscount(product, 10));

  const order = buildOrderRecord({
    customerId: admin.id,
    items: catalog.map((product) => ({
      productId: product.id,
      quantity: 1,
      unitPrice: product.price,
    })),
  });

  return {
    admin: updateUserRole(admin, 'trainer'),
    catalog,
    order: markOrderShipped(order),
  };
}

module.exports = {
  bootstrapDemoData,
  buildUserRecord,
  buildProductRecord,
  buildOrderRecord,
};
