------------------------------------------------------------------------

editor_options: markdown: wrap: 72 ---

------------------------------------------------------------------------

editor_options: markdown: wrap: 72 ---

# Nightingale Rose Diagram Digitizer

## Overview

This application digitizes Florence Nightingale's historical rose diagram by allowing users to click directly on the image to extract radius measurements for each monthly wedge. It was built incrementally across six stages, from basic image display to a fully interactive tool with undo and data export.

## Requirements

Python 3.7 or higher. Install dependencies:

```         
pip install -r requirements.txt
```

## How to Run

1.  Place Nightingale-mortality.jpg in the same folder as digitizer.py

2.  Open Terminal, navigate to the project folder, and run:

    python digitizer.py

    If python is not found, try:

    python3 digitizer.py

## How to Use

### Step 1: Set center points

- Click the center of the RIGHT chart (April 1854 circle)
- Click the center of the LEFT chart (April 1855 circle)
- A green dot confirms each center point

### Step 2: Capture data for each month

The status bar at the bottom of the image shows which month and color layer to click next. The fixed order is: 1. Click the outer edge of the BLUE region (disease deaths) 2. Click the outer edge of the RED region (wound deaths) 3. Click the outer edge of the BLACK region (other deaths)

A colored dot and line appear after each click to confirm the capture.

### Step 3: Navigate precisely

- Use the zoom and pan buttons in the toolbar for difficult areas
- Press Z or click the Undo button to remove the last captured point
- Progress is auto-saved after every single click

### Step 4: Export

Click Export CSV to generate output_data.csv. A summary table also prints to the terminal.

## Output Format

output_data.csv contains one row per month with 8 columns:

```         
month, center_right_x, center_right_y, center_left_x, center_left_y,
disease_radius, wounds_radius, other_radius
```

Radii are in pixels measured from the chart center to the outer edge of each color layer. Center coordinates are included in every row so measurements can be verified or recalculated later.

## Resuming a Session

Progress is saved to progress.json after every click. If the application is closed, reopen it and it will resume automatically from where you left off. To start a fresh session, delete progress.json.

## File Structure

```         
digitizer.py               Main application
requirements.txt           Python dependencies
Nightingale-mortality.jpg  Source diagram image
output_data.csv            Exported results
progress.json              Auto-saved session
planning_document.md       Project design document
README.md                  This file
walkthrough/               Screenshots of the application in use
```

## Challenges and Reflections

The most significant challenge was color ambiguity in the original image. The diagram uses faded, uneven tones that are inconsistent across wedges, making it impossible to use automated color detection reliably. For example, the blue regions vary considerably in saturation across different months, and some wedges appear to have their color layers in unexpected orders, with black on the outside and pink closer to the center. This required careful visual inspection for every single wedge.

A second major challenge was precision. Getting click points to land accurately on the correct layer boundary required repeated attempts and frequent use of the undo function. The zoom toolbar helped significantly for small or ambiguous wedges.

The entire digitization process took over eight hours across multiple sessions. A recurring pattern was completing a portion of the work, returning the next day, and discovering that earlier measurements needed correction. The auto-save and resume features were essential for managing this iterative process without losing progress.

## Possible Improvements

- Add a grid overlay or angle guide to help align clicks to the correct wedge midline
- Display a zoomed inset view of the current wedge being captured
- Add color highlighting to indicate which layer boundary should be clicked next, reducing ambiguity for wedges with unusual color ordering
- Allow direct numeric input as an alternative to clicking, for cases where the boundary is too ambiguous to click precisely

## Reflection

The click-based interaction model worked well overall. Having the status bar update after every click made it easy to track progress, and the auto-save feature meant that closing and reopening the application never caused any data loss. The undo function was essential — without it, a single misclick would have required restarting an entire month. The zoom and pan toolbar also helped significantly when trying to identify the exact boundary of small or ambiguous wedges.

The most challenging aspect was color ambiguity in the original image. The diagram uses faded, uneven tones that vary considerably across different wedges, making it impossible to rely on automated color detection. Some wedges appeared to have their color layers in unexpected orders, with black on the outside instead of the inside, which required careful visual inspection every time. Achieving accurate clicks on the correct layer boundary took many attempts and the process took over eight hours across multiple sessions. A recurring pattern was completing a portion of the work, returning later, and discovering that earlier measurements needed correction. If this tool were to be improved, adding a zoom inset for the current wedge and an angle guide overlay would significantly reduce the time and effort required.
