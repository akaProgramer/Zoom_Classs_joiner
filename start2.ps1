

# The name of your scheduled task.
$taskName = "ExportAppLog"

# Describe t
he scheduled task.
$description = "Export the 10 newest events in the application log"

# Register the scheduled task
Register-ScheduledTask `
    -TaskName $taskName `
    -Action $taskAction `
    -Trigger $taskTrigger `
    -Description $description