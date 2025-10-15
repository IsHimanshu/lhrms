frappe.router.on("change", () => {
    const route = frappe.get_route();

    if (route[0] === "dashboard-view" && route[1] === "Project") {
        console.log("📊 Project Dashboard loaded");

        const check_charts = setInterval(() => {
            const containers = $(".chart-container");

            if (containers.length) {
                clearInterval(check_charts);
                console.log("✅ Found chart containers:", containers.length);

                containers.each((i, el) => {
                    const svg = $(el).find("svg.frappe-chart")[0];
                    if (!svg) return;

                    svg.addEventListener("click", (evt) => {
                        const target = evt.target;

                        // bar/circle click
                        if (target.tagName === "rect" || target.tagName === "circle") {
                            const projLabel = $(svg)
                                .find("g.x.axis text")
                                .map((i, t) => t.textContent)
                                .get()[target.dataset.pointIndex || i];

                            console.log("🎯 Redirecting to Project:", projLabel);
                            if (projLabel) {
                                frappe.set_route("Form", "Project", projLabel);
                            }
                        }

                        // x-axis label click
                        if (target.tagName === "text" && target.closest(".x.axis")) {
                            const projLabel = target.textContent;
                            console.log("🎯 Redirecting to Project:", projLabel);
                            if (projLabel) {
                                frappe.set_route("Form", "Project", projLabel);
                            }
                        }
                    });
                });
            }
        }, 500);
    }
});
