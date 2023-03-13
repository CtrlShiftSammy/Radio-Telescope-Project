

#include "stdafx.h"
#include "ProgressBar.h"



// Paint the progress bar in response to a paint message
void ProgressBar::paint (CDC& dc)
{
    paintBackground (dc);
    paintStatus (dc);
}


// Paint the background of the progress bar region
void ProgressBar::paintBackground (CDC& dc)
{
    CBrush      brshBackground;
    CPen        penGray     (PS_SOLID, 1, RGB (128, 128, 128));
    CPen        penWhite    (PS_SOLID, 1, RGB (255, 255, 255));

    VERIFY (brshBackground.CreateSolidBrush (::GetSysColor (COLOR_BTNFACE)));

    dc.FillRect (m_bounds, &brshBackground);
    
    CPen    *pOldPen;
            
    pOldPen = dc.SelectObject (&penGray);
    {
        dc.MoveTo (m_bounds.left, m_bounds.top);
        dc.LineTo (m_bounds.left + m_bounds.Width () -1, m_bounds.top);

        dc.MoveTo (m_bounds.left, m_bounds.top);
        dc.LineTo (m_bounds.left, m_bounds.top + m_bounds.Height () -1);

    }
    dc.SelectObject (&penWhite);
    {
        dc.MoveTo (m_bounds.left + m_bounds.Width () -1, m_bounds.top);
        dc.LineTo (m_bounds.left + m_bounds.Width () -1, m_bounds.top + m_bounds.Height () -1);

        dc.MoveTo (m_bounds.left, m_bounds.top + m_bounds.Height () -1);
        dc.LineTo (m_bounds.left + m_bounds.Width () -1, m_bounds.top + m_bounds.Height () -1);

    }
    dc.SelectObject (pOldPen);

}


// Paint the actual status of the progress bar
void ProgressBar::paintStatus (CDC& dc)
{
    if (m_progress <= 0)
        return;

    CBrush      brshStatus;
    CRect       rect (m_bounds.left, m_bounds.top, 
                    m_bounds.left + m_progressX, m_bounds.bottom);

    COLORREF    statusColor = getStatusColor ();

    VERIFY (brshStatus.CreateSolidBrush (statusColor));

    rect.DeflateRect (1, 1);
    dc.FillRect (rect, &brshStatus);

}


// Paint the current step
void ProgressBar::paintStep (int startX, int endX)
{
    // kludge: painting the whole region on each step
    m_baseWindow->RedrawWindow (m_bounds);
    m_baseWindow->UpdateWindow ();

}


// Setup the progress bar for execution over a total number of steps
void ProgressBar::start (int total)
{
    m_total = total;
    reset ();
}


// Take one step, indicating whether it was a successful step
void ProgressBar::step (bool successful)
{
    m_progress++;

    int x = m_progressX;

    m_progressX = scale (m_progress);

    if (!m_error && !successful)
    {
        m_error = true;
        x = 1;
    }

    paintStep (x, m_progressX);

}


// Map from steps to display units
int ProgressBar::scale (int value)
{
    if (m_total > 0)
        return max (1, value * (m_bounds.Width () - 1) / m_total);

    return value;

}


// Reset the progress bar
void ProgressBar::reset ()
{
    m_progressX     = 1;
    m_progress      = 0;
    m_error         = false;

    m_baseWindow->RedrawWindow (m_bounds);
    m_baseWindow->UpdateWindow ();

}

