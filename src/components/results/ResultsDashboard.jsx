import { motion } from 'framer-motion'
import {
  RadarChart,
  Radar,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Cell,
} from 'recharts'
import { Zap, TrendingUp, TrendingDown, RotateCcw } from 'lucide-react'
import ScoreCard from './ScoreCard'
import SkillCard from './SkillCard'
import SuggestionCard from './SuggestionCard'
import SummaryCard from './SummaryCard'
import ChartCard from './ChartCard'

const RADAR_COLORS = ['#3B82F6', '#06B6D4']
const BAR_COLORS = ['#22C55E', '#EF4444']

function CustomTooltip({ active, payload, label }) {
  if (!active || !payload) return null
  return (
    <div className="glass-card rounded-xl px-3 py-2 text-xs shadow-xl">
      <p className="text-white font-medium mb-1">{label}</p>
      {payload.map((entry, i) => (
        <p key={i} style={{ color: entry.color }}>
          {entry.name}: {entry.value}
        </p>
      ))}
    </div>
  )
}

export default function ResultsDashboard({ data, onReset }) {
  const {
    atsScore,
    sectionScores,
    matchedSkills,
    missingSkills,
    strengths,
    weaknesses,
    suggestions,
    summary,
  } = data

  const radarData = [
    { subject: 'Keyword Match', score: sectionScores.keywordMatch, fullMark: 100 },
    { subject: 'Skill Match', score: sectionScores.skillMatch, fullMark: 100 },
    { subject: 'Experience', score: sectionScores.experience, fullMark: 100 },
    { subject: 'Education', score: sectionScores.education, fullMark: 100 },
    { subject: 'Formatting', score: sectionScores.formatting, fullMark: 100 },
  ]

  const barData = [
    { name: 'Matched', count: matchedSkills.length },
    { name: 'Missing', count: missingSkills.length },
  ]

  return (
    <div className="w-full space-y-8">
      <motion.div
        initial={{ opacity: 0, y: -12 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4"
      >
        <div>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-white">
            Analysis <span className="gradient-text">Results</span>
          </h2>
          <p className="text-sm text-gray-400 mt-1">
            Detailed breakdown of your resume performance
          </p>
        </div>
        <button
          onClick={onReset}
          className="flex items-center gap-2 px-4 py-2.5 text-sm font-semibold rounded-xl glass text-gray-300 hover:text-white hover:bg-white/10 transition-all duration-300 flex-shrink-0"
        >
          <RotateCcw size={16} />
          New Analysis
        </button>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1">
          <ScoreCard
            score={atsScore}
            label="ATS Score"
            subtitle="Overall resume compatibility score"
            size="lg"
            className="h-full"
          />
        </div>
        <div className="lg:col-span-2 grid grid-cols-2 sm:grid-cols-3 gap-4">
          <ScoreCard score={sectionScores.keywordMatch} label="Keyword Match" />
          <ScoreCard score={sectionScores.skillMatch} label="Skill Match" />
          <ScoreCard score={sectionScores.experience} label="Experience" />
          <ScoreCard score={sectionScores.education} label="Education" />
          <ScoreCard score={sectionScores.formatting} label="Formatting" />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <ChartCard
          title="Score Distribution"
          subtitle="Performance across all sections"
        >
          <ResponsiveContainer width="100%" height={280}>
            <RadarChart data={radarData}>
              <PolarGrid stroke="rgba(255,255,255,0.06)" />
              <PolarAngleAxis
                dataKey="subject"
                tick={{ fill: '#9CA3AF', fontSize: 11 }}
                stroke="rgba(255,255,255,0.06)"
              />
              <PolarRadiusAxis
                angle={30}
                domain={[0, 100]}
                tick={{ fill: '#6B7280', fontSize: 10 }}
                stroke="rgba(255,255,255,0.06)"
              />
              <Radar
                name="Score"
                dataKey="score"
                stroke={RADAR_COLORS[0]}
                fill={RADAR_COLORS[0]}
                fillOpacity={0.15}
                strokeWidth={2}
              />
            </RadarChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard
          title="Skill Match Overview"
          subtitle="Matched vs missing skills count"
        >
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={barData} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
              <XAxis
                dataKey="name"
                tick={{ fill: '#9CA3AF', fontSize: 12 }}
                axisLine={false}
                tickLine={false}
              />
              <YAxis
                tick={{ fill: '#6B7280', fontSize: 11 }}
                axisLine={false}
                tickLine={false}
                allowDecimals={false}
              />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="count" radius={[6, 6, 0, 0]} barSize={48}>
                {barData.map((entry, i) => (
                  <Cell key={i} fill={BAR_COLORS[i]} fillOpacity={0.8} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <SkillCard title="Matched Skills" skills={matchedSkills} type="matched" />
        <SkillCard title="Missing Skills" skills={missingSkills} type="missing" />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <SuggestionCard
          title="Resume Strengths"
          items={strengths}
          icon={TrendingUp}
        />
        <SuggestionCard
          title="Weaknesses"
          items={weaknesses}
          icon={TrendingDown}
        />
      </div>

      <SuggestionCard
        title="Improvement Suggestions"
        items={suggestions}
        icon={Zap}
      />

      <SummaryCard title="Resume Summary" summary={summary} />
    </div>
  )
}
