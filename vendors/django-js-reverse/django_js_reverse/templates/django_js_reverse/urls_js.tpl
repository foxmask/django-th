this.{{ js_var_name }} = (function () {

    function Urls() {}

    Urls._instance = {
        url_patterns:{}
    };

    Urls._get_url = function (url_pattern) {
        var self = this._instance
        return function () {
            var index, url, url_arg, url_args, _i, _len, _ref;
            _ref = self.url_patterns[url_pattern], url = _ref[0], url_args = _ref[1];
            for (index = _i = 0, _len = url_args.length; _i < _len; index = ++_i) {
                url_arg = url_args[index];
                url = url.replace("%(" + url_arg + ")s", arguments[index] || '');
            }
            return '{{url_prefix|escapejs}}' + url;
        };
    };

    Urls.init = function () {
        var name, pattern, self, url_patterns, _i, _len, _ref;
        url_patterns = [
            {% for name, pattern in urls %}
                [
                    '{{name|escapejs}}', ['{{pattern.0|escapejs}}', [{% for arg in pattern.1 %}'{{ arg|escapejs }}'{% if not forloop.last %},{% endif %}{% endfor %}]]
                ]{% if not forloop.last %},{% endif %}
            {% endfor %}
        ];
        self = this._instance;
        self.url_patterns = {};
        for (_i = 0, _len = url_patterns.length; _i < _len; _i++) {
            _ref = url_patterns[_i], name = _ref[0], pattern = _ref[1];
            self.url_patterns[name] = pattern;
            this[name] = this._get_url(name);
        }
        return self;
    };

    return Urls;
})();

this.{{ js_var_name }}.init();


