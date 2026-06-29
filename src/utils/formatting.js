export function formatPercentage(value) {
  return `${value >= 0 ? '+' : ''}${value.toFixed(2)}%`
}

export function formatNumber(value) {
  return new Intl.NumberFormat('en-US').format(value)
}
