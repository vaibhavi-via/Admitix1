import { APP_NAME } from '../utils/constants'

export default function Footer() {
  return (
    <footer className="border-t border-gray-200 bg-white px-4 py-3 text-center text-xs text-gray-500">
      © {new Date().getFullYear()} {APP_NAME}. Built with the React Student Starter Kit.
    </footer>
  )
}
