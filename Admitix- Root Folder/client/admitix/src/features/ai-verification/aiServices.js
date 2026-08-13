import api from '../../api/axios'

export function extractDocumentOCR(file) {
  const formData = new FormData()
  formData.append('file', file)
  return api.post('/ai/ocr', formData).then((res) => res.data)
}

export function verifyDocumentWithAI(file) {
  const formData = new FormData()
  formData.append('file', file)
  return api.post('/ai/document-verification', formData).then((res) => res.data)
}

export function crossVerifyDocuments(files) {
  const formData = new FormData()
  files.forEach((file) => formData.append('files', file))
  return api.post('/ai/cross-document-verification', formData).then((res) => res.data)
}
