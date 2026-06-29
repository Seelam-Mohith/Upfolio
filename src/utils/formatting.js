export function formatCurrency(value) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(value)
}

export function formatPercentage(value) {
  return `${value >= 0 ? '+' : ''}${value.toFixed(2)}%`
}

export function formatNumber(value) {
  return new Intl.NumberFormat('en-US').format(value)
}
