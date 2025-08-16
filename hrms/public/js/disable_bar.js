(function () {
    function hideSearchBarIfNotAdmin() {
        if (!frappe.session || !frappe.session.user || frappe.session.user === 'Administrator') return;

        console.log("Non Admin Detected:", frappe.session.user);

        const hideBar = () => {
            const bar = document.querySelector('.search-bar');
            if (bar) {
                bar.style.display = 'none';
            }
        };

        hideBar();

        // Watch for dynamic addition
        const observer = new MutationObserver(() => hideBar());
        observer.observe(document.body, { childList: true, subtree: true });

        // Disable Ctrl+K
        document.addEventListener("keydown", function (e) {
            if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
                e.preventDefault();
                frappe.show_alert("Search is disabled for your role.");
            }
        });

        // Disable programmatic search
        if (frappe.search?.utils?.search) {
            frappe.search.utils.search = async function () {
                return frappe.throw(__('Search is disabled for your account.'));
            };
        }
    }

    // Wait until frappe.session.user is defined
    const wait = setInterval(() => {
        if (typeof frappe !== "undefined" && frappe.session && frappe.session.user) {
            clearInterval(wait);
            hideSearchBarIfNotAdmin();
        }
    }, 100);
})();
