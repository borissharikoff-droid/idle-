import { ProgressBar } from './ProgressBar'

interface SkillPanelProps {
  level: number
  xp: number
  xpInLevel: number
  xpNeeded: number
}

export function SkillPanel({ level, xp, xpInLevel, xpNeeded }: SkillPanelProps) {
  const progress = xpNeeded > 0 ? xpInLevel / xpNeeded : 1

  return (
    <div className="bg-[#16213e] rounded-xl p-4 border border-gray-700">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          <span className="text-xl">⛏️</span>
          <span className="font-pixel text-xs text-yellow-400">MINING</span>
        </div>
        <span className="font-pixel text-lg text-yellow-400">Lv.{level}</span>
      </div>

      <ProgressBar progress={progress} color="#f59e0b" height="h-3" />

      <div className="flex justify-between mt-2 text-xs text-gray-400">
        <span>{xpInLevel.toLocaleString()} / {xpNeeded.toLocaleString()} XP</span>
        <span>Total: {xp.toLocaleString()}</span>
      </div>

      {level >= 100 && (
        <div className="mt-2 text-center">
          <span className="font-pixel text-xs text-yellow-400">✨ MAX LEVEL ✨</span>
        </div>
      )}
    </div>
  )
}
