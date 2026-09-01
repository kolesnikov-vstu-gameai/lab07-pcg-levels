using UnityEngine;
using UnityEngine.Tilemaps;

namespace Lab07.PCG
{
    /// <summary>Каркас генератора: детерминизм через seed, вывод на Tilemap. Порт алгоритма — из bsp.py.</summary>
    public class DungeonGenerator : MonoBehaviour
    {
        [SerializeField] private int seed = 0;
        [SerializeField] private int width = 64, height = 48;
        [SerializeField] private Tilemap tilemap;
        [SerializeField] private TileBase wall, floor;

        [ContextMenu("Generate")]
        public void Generate()
        {
            var rng = new System.Random(seed);
            var grid = new int[height, width];
            // TODO: BSP / клеточный автомат — заполните grid (1 = стена, 0 = пол)
            tilemap.ClearAllTiles();
            for (int y = 0; y < height; y++)
                for (int x = 0; x < width; x++)
                    tilemap.SetTile(new Vector3Int(x, y, 0), grid[y, x] == 1 ? wall : floor);
        }
    }
}
