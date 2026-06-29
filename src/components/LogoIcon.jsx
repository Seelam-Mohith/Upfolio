export default function LogoIcon({ size = 36 }) {
  return (
    <div
      className="relative flex items-center justify-center"
      style={{ width: size, height: size }}
    >
      <svg
        width={size}
        height={size}
        viewBox="0 0 36 36"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <rect width="36" height="36" rx="10" fill="#F1F5F9" />
        <path
          d="M10 26l16-16m-4 0h4v4"
          stroke="#0F172A"
          strokeWidth="2.5"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    </div>
  )
}
