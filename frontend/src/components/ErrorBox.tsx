type Props = {
  message: string
  onRetry: () => void
}

function ErrorBox({ message, onRetry }: Props) {
  return (
    <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
      <p className="font-semibold text-red-800 mb-1">Something went wrong</p>
      <p className="text-sm text-red-700 mb-1">{message}</p>
      <p className="text-xs text-gray-500 mb-4">
        Check that the backend server is running at http://127.0.0.1:8000
      </p>
      <button
        onClick={onRetry}
        className="bg-red-600 text-white text-sm px-4 py-2 rounded-md hover:bg-red-700 transition"
      >
        Try again
      </button>
    </div>
  )
}

export default ErrorBox