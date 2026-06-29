import * as Icons from 'lucide-react'

export default function FeatureIcon({ icon, gradient }) {
  const LucideIcon = Icons[icon] || Icons.HelpCircle

  return (
    <div
      className={`inline-flex items-center justify-center w-12 h-12 rounded-xl bg-gradient-to-br ${gradient} p-2.5`}
    >
      <LucideIcon className="text-white" size={24} />
    </div>
  )
}
