export default function LogoIcon({ size = 36, className = '' }) {
  return (
    <img
      src="/logo-icon.svg"
      alt="Upfolio"
      width={size}
      height={size}
      className={className}
    />
  )
}
