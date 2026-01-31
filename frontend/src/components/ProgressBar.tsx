interface ProgressBarProps {
  progress: number // 0 to 1
  color?: string
  showPercentage?: boolean
  height?: string
}

export function ProgressBar({ 
  progress, 
  color = '#5dadec', 
  showPercentage = false,
  height = 'h-4'
}: ProgressBarProps) {
  const percentage = Math.round(progress * 100)

  return (
    <div className="relative">
      <div className={`w-full ${height} bg-[#1a1a2e] rounded-full overflow-hidden border border-gray-600`}>
        <div
          className="h-full rounded-full transition-all duration-100 relative overflow-hidden"
          style={{
            width: `${percentage}%`,
            backgroundColor: color,
          }}
        >
          {/* Shimmer effect */}
          <div className="absolute inset-0 progress-shimmer" />
        </div>
      </div>
      
      {showPercentage && (
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="font-pixel text-[10px] text-white drop-shadow-lg">
            {percentage}%
          </span>
        </div>
      )}
    </div>
  )
}
