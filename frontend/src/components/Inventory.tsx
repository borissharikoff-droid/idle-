import { OreData } from '../App'

interface InventoryProps {
  ores: OreData[]
  inventory: Record<string, number>
}

export function Inventory({ ores, inventory }: InventoryProps) {
  return (
    <div className="bg-[#16213e] rounded-xl p-4 border border-gray-700">
      <h3 className="font-pixel text-xs text-gray-400 mb-4 flex items-center gap-2">
        <span>📦</span> INVENTORY
      </h3>

      <div className="grid grid-cols-3 gap-3">
        {ores.map((ore) => {
          const qty = inventory[ore.id] || 0
          const isEmpty = qty === 0

          return (
            <div
              key={ore.id}
              className={`
                relative p-3 rounded-lg text-center transition-all
                ${isEmpty 
                  ? 'bg-[#1a1a2e] opacity-50' 
                  : 'bg-[#1a1a2e] hover:bg-[#222244]'
                }
                ${ore.unlocked ? '' : 'grayscale'}
              `}
            >
              {/* Ore Display */}
              <div 
                className="w-12 h-12 mx-auto rounded-lg flex items-center justify-center mb-2"
                style={{ 
                  backgroundColor: `${ore.color}20`,
                  boxShadow: isEmpty ? 'none' : `0 0 15px ${ore.color}30`
                }}
              >
                <span 
                  className="font-pixel text-sm"
                  style={{ color: ore.color }}
                >
                  {ore.ascii}
                </span>
              </div>

              {/* Quantity */}
              <p className="font-pixel text-sm" style={{ color: ore.color }}>
                {qty.toLocaleString()}
              </p>
              
              <p className="text-[10px] text-gray-500 mt-1 truncate">
                {ore.name.replace(' Ore', '')}
              </p>

              {/* Locked Overlay */}
              {!ore.unlocked && (
                <div className="absolute inset-0 flex items-center justify-center bg-black/50 rounded-lg">
                  <span className="text-xl">🔒</span>
                </div>
              )}
            </div>
          )
        })}
      </div>

      {/* Total Value (placeholder for future trading) */}
      <div className="mt-4 pt-4 border-t border-gray-700">
        <div className="flex items-center justify-between text-xs">
          <span className="text-gray-400">Total Ores</span>
          <span className="font-pixel text-yellow-400">
            {Object.values(inventory).reduce((a, b) => a + b, 0).toLocaleString()}
          </span>
        </div>
      </div>
    </div>
  )
}
