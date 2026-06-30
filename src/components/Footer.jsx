import { Bug, GitBranch, Mail } from 'lucide-react'
import LogoIcon from './LogoIcon'

export default function Footer() {
  return (
    <footer className="mt-16 border-t border-white/10 bg-white/5 backdrop-blur-xl">
      <div className="mx-auto w-full max-w-7xl px-4 py-8 sm:px-6">
        <div className="flex flex-col gap-8 md:flex-row md:items-start md:justify-between">
          <div className="max-w-xl">
            <div className="flex items-center gap-3">
              <LogoIcon size={36} />
              <div>
                <h3 className="text-lg font-bold text-white">Upfolio</h3>
                <p className="text-sm text-gray-400">
                  AI-powered resume analysis.
                </p>
              </div>
            </div>

            <p className="mt-4 text-sm leading-6 text-gray-400">
              Upload your resume and get instant AI-powered insights, ATS
              compatibility scores, and optimization suggestions to land
              more interviews.
            </p>
          </div>

          <div className="space-y-6">
            <div className="grid gap-8 sm:grid-cols-2">
              <div>
                <h4 className="text-sm font-semibold uppercase tracking-[0.18em] text-gray-300">
                  Contact
                </h4>
                <a
                  href="mailto:seelammohith2222@gmail.com"
                  className="mt-3 flex items-center gap-3 text-sm text-gray-400 transition-colors hover:text-blue-300"
                >
                  <Mail className="h-4 w-4" />
                  <span>seelammohith2222@gmail.com</span>
                </a>
              </div>

              <div>
                <h4 className="text-sm font-semibold uppercase tracking-[0.18em] text-gray-300">
                  Creator
                </h4>
                <a
                  href="https://github.com/Seelam-Mohith"
                  target="_blank"
                  rel="noreferrer"
                  className="mt-3 flex items-center gap-3 text-sm text-gray-400 transition-colors hover:text-blue-300"
                >
                  <GitBranch className="h-4 w-4" />
                  <span>github.com/Seelam-Mohith</span>
                </a>
              </div>
            </div>

            <div>
              <h4 className="text-sm font-semibold uppercase tracking-[0.18em] text-gray-300">
                Issues
              </h4>
              <a
                href="https://github.com/Seelam-Mohith/Upfolio/issues"
                target="_blank"
                rel="noreferrer"
                className="mt-3 flex items-center gap-3 text-sm text-gray-400 transition-colors hover:text-blue-300"
              >
                <Bug className="h-4 w-4" />
                <span>Report issues here</span>
              </a>
            </div>
          </div>
        </div>

        <div className="mt-8 border-t border-white/10 pt-4 text-xs text-gray-500">
          Built by Seelam Mohith for AI-powered resume analysis.
        </div>
      </div>
    </footer>
  )
}
