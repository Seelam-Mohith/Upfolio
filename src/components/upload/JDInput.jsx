import { cn } from '../../utils/cn'

export default function JDInput({ value, onChange, disabled, className }) {
  return (
    <div className={cn('space-y-2', className)}>
      <label className="block text-sm font-medium text-gray-300">
        Job Description{' '}
        <span className="text-gray-500 font-normal">(optional)</span>
      </label>

      <div className="relative">
        <textarea
          value={value}
          onChange={(e) => onChange(e.target.value)}
          disabled={disabled}
          rows={5}
          placeholder="Paste the job description here to get targeted keyword matching and personalized suggestions..."
          className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3.5 text-sm text-white placeholder-gray-500 resize-none transition-all duration-300 focus:outline-none focus:border-primary/50 focus:ring-1 focus:ring-primary/20 disabled:opacity-50 disabled:cursor-not-allowed"
        />

        <div className="absolute bottom-3 right-3 text-[11px] text-gray-500 tabular-nums">
          {value.length}
          <span className="text-gray-600"> / 2000</span>
        </div>
      </div>
    </div>
  )
}
