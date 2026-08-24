import axios from 'axios'

const VALID_FILE_TYPES = [
  'application/pdf',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
]

const MAX_FILE_SIZE = 10 * 1024 * 1024

function validateFile(file) {
  const extension = file.name.split('.').pop().toLowerCase()
  const isValidType =
    VALID_FILE_TYPES.includes(file.type) || ['pdf', 'docx'].includes(extension)

  if (!isValidType) {
    throw new Error('Invalid file type. Please upload a PDF or DOCX file.')
  }

  if (file.size > MAX_FILE_SIZE) {
    throw new Error('File size exceeds 10MB limit.')
  }
}

export async function uploadResume(file, jobDescription, onProgress) {
  validateFile(file)

  const formData = new FormData()
  formData.append('resume', file)
  if (jobDescription && jobDescription.trim()) {
    formData.append('job_description', jobDescription.trim())
  }

  let progressInterval
  if (onProgress) {
    let progress = 0
    progressInterval = setInterval(() => {
      progress = Math.min(progress + Math.random() * 12 + 2, 90)
      onProgress(Math.round(progress))
    }, 300)
  }

  try {
    const { data } = await axios.post('/api/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      timeout: 60000,
    })

    if (!data.success) {
      throw new Error(data.error || 'Analysis failed. Please try again.')
    }

    onProgress?.(100)

    return {
      success: true,
      data: {
        fileName: file.name,
        fileSize: file.size,
        fileType: file.type,
        pages: data.pages,
        ...data.analysis,
        parsedData: data.parsedData,
      },
    }
  } catch (err) {
    const message =
      err.response?.data?.error ||
      (err.code === 'ECONNABORTED'
        ? 'The analysis took too long. Please try again.'
        : err.message)

    throw new Error(message)
  } finally {
    if (progressInterval) clearInterval(progressInterval)
  }
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
