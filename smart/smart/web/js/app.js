// Smart Shiksha Dashboard Logic

document.addEventListener('DOMContentLoaded', () => {
    fetchDashboardStats();
    fetchStudentData();
});

const API_BASE = 'http://127.0.0.1:8000/api/v1';

async function fetchDashboardStats() {
    try {
        const response = await fetch(`${API_BASE}/analytics/dashboard`);
        const data = await response.json();

        // Update Stats Cards (assuming order: Avg Score, Active, Tests)
        const stats = document.querySelectorAll('.stat-card h2');
        if (stats.length >= 3) {
            stats[0].innerText = `${data.avg_class_score}%`;
            stats[1].innerText = `${data.active_students}/${data.total_students}`;
            stats[2].innerText = `${data.tests_completed}`;
        }
    } catch (e) {
        console.error("Failed to fetch stats", e);
    }
}

async function fetchStudentData() {
    const tableBody = document.getElementById('student-table-body');
    tableBody.innerHTML = '<tr><td colspan="4" style="text-align:center">Loading real data...</td></tr>';

    try {
        const response = await fetch(`${API_BASE}/users`);
        const students = await response.json();

        // Clear loading
        tableBody.innerHTML = '';

        students.forEach(student => {
            const row = document.createElement('tr');

            // Logic to determine status color based on last active
            let isOnline = student.last_active !== 'Never';
            let statusColor = isOnline ? '#10B981' : '#64748B';
            let statusText = isOnline ? 'Active' : 'Inactive';

            row.innerHTML = `
                <td>
                    <div style="font-weight: 600;">${student.username}</div>
                    <div style="font-size: 0.8rem; color: #64748B;">ID: ${student.id.substring(0, 8)}...</div>
                </td>
                <td>
                    <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: ${statusColor}; margin-right: 6px;"></span>
                    ${statusText}
                </td>
                <td style="color: #94A3B8;">${student.last_active}</td>
                <td>
                    <span style="background: rgba(255,255,255,0.1); padding: 4px 8px; border-radius: 4px;">
                        ${student.avg_score}%
                    </span>
                </td>
            `;

            tableBody.appendChild(row);
        });
    } catch (e) {
        tableBody.innerHTML = '<tr><td colspan="4" style="text-align:center; color: #EF4444">Failed to load data. Is Backend running?</td></tr>';
        console.error(e);
    }
}
