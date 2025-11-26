#!/bin/bash
# Continuous monitoring and database update script
# Monitors Parallel Task research and updates database automatically

echo "=============================================================================="
echo "LATERAL ENTRY RESEARCH MONITOR & AUTO-UPDATE"
echo "=============================================================================="
echo "Started at: $(date)"
echo ""
echo "Monitoring Tasks:"
echo "  - Task 1: 2024 Batch Research (trun_81c34e5f8d8f4cba810ed818395e75c7)"
echo "  - Task 2: 2023 Batch Research (trun_81c34e5f8d8f4cba9095ea13193f8156)"
echo "=============================================================================="
echo ""

# URLs for the tasks
TASK_2024="https://platform.parallel.ai/view/task-run/trun_81c34e5f8d8f4cba810ed818395e75c7"
TASK_2023="https://platform.parallel.ai/view/task-run/trun_81c34e5f8d8f4cba9095ea13193f8156"

ITERATION=0
MAX_ITERATIONS=60  # Run for ~30 minutes

echo "📋 Tasks are running in background..."
echo "   View 2024 Batch: $TASK_2024"
echo "   View 2023 Batch: $TASK_2023"
echo ""
echo "🔄 Will check status every 30 seconds (max $MAX_ITERATIONS checks)"
echo "=============================================================================="
echo ""

while [ $ITERATION -lt $MAX_ITERATIONS ]; do
    ITERATION=$((ITERATION + 1))
    
    echo ""
    echo "======================================================================"
    echo "🔄 Check #$ITERATION at $(date +%H:%M:%S)"
    echo "======================================================================"
    
    # Get current database stats
    echo "📊 Current Database Statistics:"
    sqlite3 /home/ubuntu/projects/lateral-entry-portal/database/lateral_entry.db << 'EOF'
.mode column
SELECT batch_year, COUNT(*) as count FROM lateral_entrants GROUP BY batch_year;
EOF
    
    echo ""
    echo "⏳ Research tasks are still running..."
    echo "   Check progress at the URLs above"
    echo ""
    
    # Show countdown
    if [ $ITERATION -lt $MAX_ITERATIONS ]; then
        echo "⏸️  Waiting 30 seconds before next check..."
        sleep 30
    fi
done

echo ""
echo "=============================================================================="
echo "✅ Monitoring period complete at $(date)"
echo "=============================================================================="
echo ""
echo "📊 Final Database Statistics:"
sqlite3 /home/ubuntu/projects/lateral-entry-portal/database/lateral_entry.db << 'EOF'
.mode column
.headers on
SELECT batch_year, COUNT(*) as total FROM lateral_entrants GROUP BY batch_year;
SELECT 'TOTAL' as batch_year, COUNT(*) as total FROM lateral_entrants;
EOF

echo ""
echo "💡 To manually check task progress, visit:"
echo "   2024 Batch: $TASK_2024"
echo "   2023 Batch: $TASK_2023"
echo ""
echo "✅ Monitor script completed!"
