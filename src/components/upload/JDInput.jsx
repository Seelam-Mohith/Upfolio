import { cn } from '../../utils/cn'
import { jobDescriptions } from '../../data/jobDescriptions'

export default function JDInput({ value, onChange, disabled, className }) {
  return (
    <div className={cn('space-y-2', className)}>
      <label className="block text-sm font-medium text-gray-300">
        Job Description{' '}
        <span className="text-gray-500 font-normal">(optional)</span>
      </label>

      <div className="flex flex-wrap gap-2">
        {jobDescriptions.map((jd) => (
          <button
            key={jd.id}
            type="button"
            onClick={() => onChange(jd.description)}
            disabled={disabled}
            className={cn(
              'px-3 py-1.5 text-xs rounded-lg border transition-all duration-200',
              value === jd.description
                ? 'bg-primary/20 border-primary/50 text-primary-300'
                : 'bg-white/5 border-white/10 text-gray-400 hover:border-white/20 hover:text-gray-200',
              disabled && 'opacity-50 cursor-not-allowed'
            )}
          >
            {jd.title}
          </button>
        ))}
      </div>

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
