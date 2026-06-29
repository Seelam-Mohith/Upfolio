import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { FileText, CheckCircle, Sparkles, ArrowRight } from 'lucide-react'
import Button from './Button'

const floatingIcons = [
  { Icon: FileText, delay: 0, x: '-20%', y: '10%' },
  { Icon: CheckCircle, delay: 0.3, x: '25%', y: '-15%' },
  { Icon: Sparkles, delay: 0.6, x: '-30%', y: '-25%' },
]

export default function Hero() {
  return (
    <section className="relative min-h-screen flex items-center overflow-hidden pt-14">
      <div className="absolute inset-0 bg-grid" />
      <div className="absolute inset-0 bg-gradient-radial" />
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-primary/10 rounded-full blur-[120px]" />
      <div className="absolute bottom-1/4 right-1/4 w-[400px] h-[400px] bg-secondary/10 rounded-full blur-[100px]" />

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          <motion.div
            initial={{ opacity: 0, x: -60 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, ease: 'easeOut' }}
          >
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2, duration: 0.5 }}
              className="inline-flex items-center gap-2 glass rounded-full px-4 py-2 mb-8"
            >
              <Sparkles size={16} className="text-primary" />
              <span className="text-sm text-gray-300">
                AI-Powered Resume Analysis
              </span>
            </motion.div>

            <h1 className="text-4xl sm:text-5xl lg:text-6xl xl:text-7xl font-extrabold text-white leading-[1.1] mb-6">
              Transform Your
              <br />
              <span className="gradient-text">Resume Strategy</span>
              <br />
              with AI
            </h1>

            <p className="text-lg sm:text-xl text-gray-400 leading-relaxed mb-8 max-w-xl">
              Upfolio uses advanced machine learning to analyze, optimize, and
              perfect your resume. Get past ATS filters and land more interviews
              with AI-powered insights.
            </p>

            <Button variant="secondary" size="lg" href="#how-it-works">
              See How It Works
            </Button>


          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 60 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.2, ease: 'easeOut' }}
            className="relative hidden lg:block self-start lg:mt-6"
          >
            <div className="glass-card p-8 glow">
              <div className="space-y-6">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-semibold text-white">
                    Resume Scorecard
                  </h3>
                  <span className="text-sm text-green-400 flex items-center gap-1">
                    <CheckCircle size={14} />
                    82/100
                  </span>
                </div>

                <div className="space-y-4">
                  {[
                    { label: 'ATS Keywords', value: 88, color: 'bg-blue-500' },
                    { label: 'Formatting', value: 95, color: 'bg-cyan-500' },
                    { label: 'Impact Metrics', value: 65, color: 'bg-purple-500' },
                    { label: 'Content Density', value: 78, color: 'bg-orange-500' },
                  ].map((item) => (
                    <div key={item.label}>
                      <div className="flex justify-between text-sm mb-1">
                        <span className="text-gray-400">{item.label}</span>
                        <span className="text-white font-medium">
                          {item.value}%
                        </span>
                      </div>
                      <div className="h-2 bg-white/5 rounded-full overflow-hidden">
                        <motion.div
                          initial={{ width: 0 }}
                          animate={{ width: `${item.value}%` }}
                          transition={{ duration: 1, delay: 0.5 + item.value * 0.01 }}
                          className={`h-full rounded-full ${item.color}`}
                        />
                      </div>
                    </div>
                  ))}
                </div>

                <div className="glass rounded-xl p-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-gray-400">ATS Compatibility</span>
                    <span className="text-sm text-green-400 font-semibold">Strong Match</span>
                  </div>
                  <div className="flex gap-1">
                    {[1, 2, 3, 4, 5].map((i) => (
                      <div
                        key={i}
                        className={`h-2 flex-1 rounded-full ${
                          i <= 4 ? 'bg-green-500' : 'bg-white/10'
                        }`}
                      />
                    ))}
                  </div>
                </div>

                <Link to="/analyze" className="block">
                  <Button className="w-full justify-center mt-6" size="md">
                    Analyze Your Resume
                    <ArrowRight size={18} />
                  </Button>
                </Link>
              </div>
            </div>

            {floatingIcons.map(({ Icon, delay, x, y }) => (
              <motion.div
                key={Icon.name}
                className="absolute -z-10"
                style={{ left: `calc(50% + ${x})`, top: `calc(50% + ${y})` }}
                animate={{
                  y: [0, -10, 0],
                  opacity: [0.5, 1, 0.5],
                }}
                transition={{
                  duration: 3,
                  repeat: Infinity,
                  delay,
                  ease: 'easeInOut',
                }}
              >
                <div className="w-12 h-12 glass rounded-xl flex items-center justify-center">
                  <Icon className="text-primary" size={24} />
                </div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </div>
    </section>
  )
}
