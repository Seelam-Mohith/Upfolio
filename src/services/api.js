const MOCK_DELAY = 2500
const PROGRESS_INTERVAL = 250

function randomScore(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min
}

export async function uploadResume(file, jobDescription, onProgress) {
  const validTypes = [
    'application/pdf',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'text/plain',
  ]

  if (!validTypes.includes(file.type)) {
    throw new Error('Invalid file type. Please upload a PDF, DOCX, or TXT file.')
  }

  const maxSize = 10 * 1024 * 1024
  if (file.size > maxSize) {
    throw new Error('File size exceeds 10MB limit.')
  }

  return new Promise((resolve, reject) => {
    let progress = 0
    const interval = setInterval(() => {
      const increment = Math.random() * 18 + 2
      progress = Math.min(progress + increment, 95)
      onProgress?.(Math.round(progress))
    }, PROGRESS_INTERVAL)

    setTimeout(() => {
      clearInterval(interval)
      onProgress?.(100)

      setTimeout(() => {
        if (Math.random() > 0.1) {
          const atsScore = randomScore(60, 94)
          const sectionScores = {
            keywordMatch: randomScore(55, 95),
            skillMatch: randomScore(50, 90),
            experience: randomScore(60, 95),
            education: randomScore(55, 90),
            formatting: randomScore(45, 85),
          }

          const matchedSkills = [
            'React',
            'JavaScript',
            'Python',
            'Node.js',
            'TypeScript',
            'SQL',
            'Git',
          ]

          const missingSkills = jobDescription
            ? ['Kubernetes', 'GraphQL', 'Redis', 'AWS', 'Docker', 'CI/CD']
            : ['Kubernetes', 'GraphQL', 'Redis']

          resolve({
            success: true,
            data: {
              fileName: file.name,
              fileSize: file.size,
              fileType: file.type,
              atsScore,
              sectionScores,
              matchedSkills,
              missingSkills,
              strengths: [
                'Strong technical skill set with modern web technologies including React and Node.js',
                'Clear and well-structured work experience descriptions with relevant keywords',
                'Solid educational background in Computer Science from a reputable institution',
                'Good use of action verbs throughout experience section',
              ],
              weaknesses: [
                'Missing quantifiable achievements and specific metrics in experience descriptions',
                'No certifications or professional development mentioned',
                'Summary section lacks targeted keywords for specific roles',
                'Formatting inconsistencies detected in bullet points and section headers',
              ],
              suggestions: [
                'Add quantifiable achievements with specific metrics (e.g., "Increased performance by 40%")',
                'Include relevant certifications (AWS, Google Cloud, or industry-specific certs)',
                'Strengthen your professional summary with role-specific keywords from job descriptions',
                'Standardize formatting across all sections for a cleaner, more professional look',
                'Add a dedicated skills section with proficiency levels for better ATS parsing',
                'Include links to GitHub portfolio, LinkedIn, and personal website',
              ],
              summary:
                'Experienced software engineer with 5+ years in full-stack development. Proficient in React, Node.js, TypeScript, and cloud technologies. Proven track record of delivering scalable web applications and leading cross-functional teams. Passionate about clean code, performance optimization, and mentoring junior developers.',
              keywordMatch: randomScore(60, 90),
              readabilityScore: randomScore(65, 95),
              keywords: matchedSkills,
              missingKeywords: missingSkills,
              parsedData: {
                name: 'John Doe',
                email: 'john.doe@email.com',
                phone: '+1 (555) 123-4567',
                location: 'San Francisco, CA',
                skills: matchedSkills,
                experience: [
                  {
                    company: 'Tech Corp',
                    role: 'Senior Software Engineer',
                    duration: '2021 - Present',
                    description:
                      'Led development of microservices architecture serving 1M+ users',
                  },
                  {
                    company: 'StartupX',
                    role: 'Full Stack Developer',
                    duration: '2018 - 2021',
                    description:
                      'Built and scaled React frontend with Node.js backend',
                  },
                ],
                education: [
                  {
                    institution: 'University of Technology',
                    degree: 'B.S. Computer Science',
                    year: '2018',
                  },
                ],
              },
            },
          })
        } else {
          reject(
            new Error(
              'Analysis failed. Please try again or upload a different file.'
            )
          )
        }
      }, 500)
    }, MOCK_DELAY)
  })
}

export async function getAnalysisHistory() {
  await new Promise((r) => setTimeout(r, 500))
  return {
    success: true,
    data: [
      {
        id: '1',
        fileName: 'resume_2024.pdf',
        date: '2024-12-15',
        atsScore: 82,
      },
      {
        id: '2',
        fileName: 'resume_v3.docx',
        date: '2024-11-20',
        atsScore: 74,
      },
    ],
  }
}

export async function deleteAnalysis(id) {
  await new Promise((r) => setTimeout(r, 300))
  return { success: true }
}
