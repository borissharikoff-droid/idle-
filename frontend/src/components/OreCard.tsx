import { OreData } from '../App'

interface OreCardProps {
  ore: OreData
  currentLevel: number
  quantity: number
  isActive: boolean
  onSelect: () => void
  disabled: boolean
}

export function OreCard({ ore, currentLevel, quantity, isActive, onSelect, disabled }: OreCardProps) {
  const isLocked = currentLevel < ore.level_required

  return (
    <button
      onClick={onSelect}
      disabled={disabled || isLocked}
      className={`
        w-full p-4 rounded-xl border transition-all text-left
        ${isActive 
          ? 'border-yellow-400 bg-yellow-400/10' 
          : isLocked
            ? 'border-gray-700 bg-[#16213e] opacity-50 cursor-not-allowed'
            : disabled
              ? 'border-gray-700 bg-[#16213e] opacity-70 cursor-not-allowed'
              : 'border-gray-700 bg-[#16213e] hover:border-gray-500 hover:bg-[#1e2a47]'
        }
      `}
    >
      <div className="flex items-center gap-4">
        {/* Ore Icon */}
        <div 
          className={`
            w-14 h-14 rounded-lg flex items-center justify-center
            ${isLocked ? 'bg-gray-800' : 'bg-[#1a1a2e]'}
          `}
          style={{ 
            boxShadow: isLocked ? 'none' : `0 0 20px ${ore.color}40`
          }}
        >
          {isLocked ? (
            <span className="text-2xl">🔒</span>
          ) : (
            <span 
              className="font-pixel text-sm"
              style={{ color: ore.color }}
            >
              {ore.ascii}
            </span>
          )}
        </div>

        {/* Ore Info */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2">
            <h3 
              className="font-pixel text-xs truncate"
              style={{ color: isLocked ? '#6b7280' : ore.color }}
            >
              {ore.name}
            </h3>
            {isActive && (
              <span className="text-xs bg-yellow-400 text-black px-2 py-0.5 rounded font-pixel">
                ACTIVE
              </span>
            )}
          </div>
          
          <p className="text-xs text-gray-400 mt-1">
            {isLocked 
              ? `Unlock at Level ${ore.level_required}`
              : ore.description
            }
          </p>

          <div className="flex items-center gap-4 mt-2 text-xs">
            <span className="text-gray-400">
              ⏱️ {ore.mining_time}s
            </span>
            <span className="text-yellow-400">
              +{ore.xp} XP
            </span>
            {!isLocked && (
              <span className="text-gray-400">
                📦 {quantity}
              </span>
            )}
          </div>
        </div>

        {/* Level Badge */}
        <div 
          className={`
            text-center px-3 py-1 rounded-lg
            ${isLocked ? 'bg-gray-800 text-gray-500' : 'bg-[#1a1a2e]'}
          `}
        >
          <p className="font-pixel text-[10px] text-gray-400">LVL</p>
          <p 
            className="font-pixel text-sm"
            style={{ color: isLocked ? '#6b7280' : ore.color }}
          >
            {ore.level_required}
          </p>
        </div>
      </div>
    </button>
  )
}
