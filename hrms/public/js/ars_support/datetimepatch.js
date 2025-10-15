
(function installDatetimePatch() {
	function apply() {
		const Ct = frappe?.ui?.form?.ControlDatetime;
		if (!Ct) return false;

		if (Ct.__patched_set_formatted_input) return true; 

		const proto = Ct.prototype;

		
		const original = proto.set_formatted_input;

		proto.set_formatted_input = function (value) {
			
			if (this.timepicker_only || !this.datepicker) return;

			
			if (typeof value === "string") {
				if (!value) {
					this.datepicker.clear();
					this.$input && this.$input.val("");
					this.last_value = "";
					return;
				}
				const v = value.toLowerCase();
				if (v === "today") value = this.get_now_date();
				else if (v === "now") value = frappe.datetime.now_datetime();
			} else if (!value) {
				this.datepicker.clear();
				this.$input && this.$input.val("");
				this.last_value = "";
				return;
			}

			
			const formatted = this.format_for_input(value);
			this.$input && this.$input.val(formatted);


			const desired = frappe.datetime.user_to_obj(formatted);
			const selected = this.datepicker.selectedDates && this.datepicker.selectedDates[0];

			const hasSeconds = this.datepicker.opts.timeFormat.indexOf("s") !== -1;
			const normalize = (d) => {
				if (!d) return d;
				const nd = new Date(d.getTime());
				if (!hasSeconds) nd.setSeconds(0, 0);
				else nd.setMilliseconds(0);
				return nd;
			};

			let should_refresh = false;


			if (this.last_value && this.last_value !== formatted) {
				should_refresh = true;
			}


			if (!should_refresh) {
				if (!selected) {
					should_refresh = true;
				} else {
					const a = normalize(selected);
					const b = normalize(desired);
					should_refresh = a.getTime() !== b.getTime();
				}
			}

			if (should_refresh) {
				this.datepicker.selectDate(desired);
			}

			this.last_value = formatted;
		};

		
		Ct.__patched_set_formatted_input = { original };
		return true;
	}


	if (!apply()) {
		const t = setInterval(() => {
			if (apply()) clearInterval(t);
		}, 50);
	}
})();
