// This is an hack to get the hover_* options translated on the
// boolean_button terminology widget. The terms are translated through
// _t(opt_terms.hover_true) or _t(opt_terms.hover_true) which will only work
// if the terms are already present in the translation map.
// This code does nothing but marks the strings as translatable
var _t = function(x) { return x; };

_t("Obtained");
_t("Non Obtained");