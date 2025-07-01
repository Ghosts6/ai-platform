export default function Error500() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 dark:bg-gray-900">
      <h1 className="text-5xl font-bold text-yellow-600 mb-4">500</h1>
      <p className="text-lg text-gray-700 dark:text-gray-200">Internal Server Error</p>
    </div>
  );
}
