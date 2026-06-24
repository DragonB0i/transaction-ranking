const API = "https://transaction-ranking.onrender.com/";

async function createTransaction() {

    const txnId =
        document.getElementById("txnId").value;

    const userId =
        Number(document.getElementById("userId").value);

    const amount =
        Number(document.getElementById("amount").value);

    try {

        const response = await fetch(
            `${API}/transaction`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    transactionId: txnId,
                    userId: userId,
                    amount: amount
                })
            }
        );

        const data = await response.json();

        alert(data.message);

        loadRanking();

    } catch (error) {

        console.log(error);

        alert("Transaction failed");
    }
}

async function loadRanking() {

    try {

        const response =
            await fetch(`${API}/ranking`);

        const rankings =
            await response.json();

        let html = "";

        rankings.forEach(user => {

            html += `
                <p>
                    Rank ${user.rank}
                    | User ${user.userId}
                    | Score ${user.score}
                    | Streak ${user.streak}
                </p>
            `;
        });

        document.getElementById(
            "ranking"
        ).innerHTML = html;

    } catch (error) {

        console.log(error);

        document.getElementById(
            "ranking"
        ).innerHTML =
            "<p>Unable to load ranking</p>";
    }
}

async function loadSummary() {

    const userId =
        document.getElementById(
            "summaryUserId"
        ).value;

    try {

        const response =
            await fetch(
                `${API}/summary/${userId}`
            );

        const user =
            await response.json();

        document.getElementById(
            "summary"
        ).innerHTML = `
            <p>Total Amount: ${user.totalAmount}</p>
            <p>Total Points: ${user.totalPoints}</p>
            <p>Bonus Points: ${user.bonusPoints}</p>
            <p>Transactions: ${user.transactionCount}</p>
            <p>Streak: ${user.currentStreak}</p>
            <p>Ranking Score: ${user.rankingScore}</p>
        `;

    } catch (error) {

        console.log(error);

        document.getElementById(
            "summary"
        ).innerHTML =
            "<p>User not found</p>";
    }
}

async function checkHealth() {

    try {

        const response =
            await fetch(`${API}/health`);

        if (response.ok) {

            document.getElementById(
                "health-status"
            ).innerHTML =
                "Backend Online";

        } else {

            document.getElementById(
                "health-status"
            ).innerHTML =
                "Backend Responded";
        }

    } catch (error) {

        console.log(error);

        document.getElementById(
            "health-status"
        ).innerHTML =
            "Backend Offline";
    }
}

window.onload = () => {

    checkHealth();

    loadRanking();
};
