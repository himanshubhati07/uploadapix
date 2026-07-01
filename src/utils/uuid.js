/**
 * Simple UUID v4 generator — avoids needing an external dependency.
 * Produces a standard RFC4122 v4 UUID string.
 */
const v4 = () => {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0;
    const v = c === 'x' ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });
};

module.exports = { v4 };