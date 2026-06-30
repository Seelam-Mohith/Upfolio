const MOCK_DELAY = 2500
const PROGRESS_INTERVAL = 250

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
          resolve({
            success: true,
            data: {
              fileName: file.name,
              fileSize: file.size,
              fileType: file.type,
              atsScore: Math.floor(Math.random() * 35) + 60,
              keywordMatch: Math.floor(Math.random() * 30) + 60,
              readabilityScore: Math.floor(Math.random() * 25) + 70,
              keywords: [
                'React',
                'JavaScript',
                'Python',
                'Node.js',
                'TypeScript',
                'SQL',
                'AWS',
                'Docker',
              ],
              missingKeywords: jobDescription
                ? ['Kubernetes', 'GraphQL', 'Redis', 'CI/CD']
                : [],
              suggestions: [
                'Add more quantifiable achievements with specific metrics',
                'Include relevant certifications and professional development',
                'Strengthen your summary section with targeted keywords',
                'Ensure consistent formatting across all sections',
              ],
              parsedData: {
                name: 'John Doe',
                email: 'john.doe@email.com',
                phone: '+1 (555) 123-4567',
                location: 'San Francisco, CA',
                skills: [
                  'React',
                  'JavaScript',
                  'Python',
                  'Node.js',
                  'TypeScript',
                ],
                experience: [
                  {
                    company: 'Tech Corp',
                    role: 'Senior Software Engineer',
                    duration: '2021 - Present',
                  },
                  {
                    company: 'StartupX',
                    role: 'Full Stack Developer',
                    duration: '2018 - 2021',
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
            new Error('Analysis failed. Please try again or upload a different file.')
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
