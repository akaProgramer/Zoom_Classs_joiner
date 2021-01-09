$taskName = "TestTask"
$action = New-ScheduledTaskAction -Execute "notepad.exe" 
$trigger = New-ScheduledTaskTrigger -Weekly -AT "11:00" -DaysOfWeek 'Monday', 'Tuesday', 'Wednesday','Thursday'
$Trigger.Repetition = $(New-ScheduledTaskTrigger -Once -RandomDelay "00:30" -At "08:00" -RepetitionDuration "12:00" -RepetitionInterval "01:00").Repetition
$inputObject = New-ScheduledTask -Action $action -Trigger $trigger -Settings $settings 
Register-ScheduledTask -TaskName $taskName -InputObject $inputObject 