.PHONY: messages compile

messages:
	pygettext3 -d messages --no-location -o tax/locales/messages.pot tax/* tax/calculators/* tax/costs/* tax/employment_types/* tax/ui/*

compile:
	for lang in tax/locales/*/; do \
		msgfmt $$lang/LC_MESSAGES/messages.po -o $$lang/LC_MESSAGES/messages.mo; \
	done
