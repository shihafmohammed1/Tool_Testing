const { test, assert, assertThrows, assertValidId } = require('./helpers/testUtils');
const { buildUserRecord, updateUserRole } = require('../src/services/userService');
const { buildProductRecord, applyDiscount } = require('../src/services/productService');
const { buildOrderRecord, markOrderShipped } = require('../src/services/orderService');

test('buildUserRecord creates a normalized user', () => {
  const user = buildUserRecord({
    firstName: 'Jamie',
    lastName: 'Lee',
    email: 'Jamie.Lee@Example.com',
  });

  assertValidId(user);
  assert.equal(user.name, 'Jamie Lee');
  assert.equal(user.email, 'jamie.lee@example.com');
});

test('buildUserRecord rejects invalid email', () => {
  assertThrows(
    () => buildUserRecord({ firstName: 'Jamie', lastName: 'Lee', email: 'bad-email' }),
    'Invalid email'
  );
});

test('updateUserRole updates role metadata', () => {
  const user = buildUserRecord({
    firstName: 'Sam',
    lastName: 'Patel',
    email: 'sam@example.com',
  });

  const updated = updateUserRole(user, 'reviewer');
  assert.equal(updated.role, 'reviewer');
  assert.ok(updated.updatedAt);
});

test('buildProductRecord stores trimmed product data', () => {
  const product = buildProductRecord({ name: '  Monitor  ', price: 249.5 });

  assertValidId(product);
  assert.equal(product.name, 'Monitor');
  assert.equal(product.price, 249.5);
});

test('buildProductRecord rejects non-positive price', () => {
  assertThrows(
    () => buildProductRecord({ name: 'Monitor', price: 0 }),
    'positive number'
  );
});

test('applyDiscount reduces price and adds label', () => {
  const product = buildProductRecord({ name: 'Headset', price: 100 });
  const discounted = applyDiscount(product, 25);

  assert.equal(discounted.price, 75);
  assert.match(discounted.label, /\$/);
});

test('buildOrderRecord calculates totals from line items', () => {
  const order = buildOrderRecord({
    customerId: 'customer-1',
    items: [
      { productId: 'p1', quantity: 2, unitPrice: 15 },
      { productId: 'p2', quantity: 1, unitPrice: 40 },
    ],
  });

  assertValidId(order);
  assert.equal(order.total, 70);
  assert.match(order.totalLabel, /\$/);
});

test('buildOrderRecord rejects empty carts', () => {
  assertThrows(
    () => buildOrderRecord({ customerId: 'customer-1', items: [] }),
    'at least one item'
  );
});

test('markOrderShipped updates status and timestamp', () => {
  const shipped = markOrderShipped(
    buildOrderRecord({
      customerId: 'customer-1',
      items: [{ productId: 'p1', quantity: 1, unitPrice: 10 }],
    })
  );

  assert.equal(shipped.status, 'shipped');
  assert.ok(shipped.shippedAt);
});
