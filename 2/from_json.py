class JSONParser(object):
    def __init__(self):
        pass

    def get_tokens(self, s, delim = ","):
    	string_started = False
    	dict_count = 0
    	arr_count = 0
        tokens = []

    	current_token_string = ""

    	for character in s:
    		if character == '\'' or character == '"':
    			if string_started:
    				string_started=False
    			else:
    				string_started=True
    		if character == '{':
    			dict_count += 1
    		if character == '}':
    			dict_count -= 1
    		if character == '[':
    			arr_count += 1
    		if character == ']':
    			arr_count -= 1
    		if delim == character and arr_count == 0 and dict_count == 0 and not string_started:
    			tokens.append(current_token_string)
    			current_token_string = ""
    			continue
    		current_token_string += character
    	if len(current_token_string) > 0:
    		tokens.append(current_token_string)

    	return tokens

    def truncate_whitespaces(self, s):
    	string_started = False
    	return_string = ""
    	for character in s:
    		if character == '\'' or character == '"':
    			if string_started:
    				string_started=False
    			else:
    				string_started=True
    		if self.is_whitespace(character) and not string_started:
    			continue
    		return_string += character
    	return return_string


    def is_whitespace(self, c):
        return (c == ' ' or c == '\n' or c == '\t')

    def get_object_from_string(self, s):
        s = self.truncate_whitespaces(s)

        if s[0] == '[':
            return self.array_from_string(s)

        if s[0] == '{':
            return self.hash_from_string(s)

        if self.is_valid_key(s):
            return eval(s)

        raise Exception('ParseError: invalid string ' + s)

    def array_from_string(self, s):
        result = []
        s = self.truncate_whitespaces(s)
        if s[0] != '[' or s[-1] != ']':
            raise Exception('ParseError: invalid json array ' + s)

        content = s[1:-1]
        for token in self.get_tokens(content):
            result.append(self.get_object_from_string(token))

        return result

    def hash_from_string(self, s):
        result = {}
        s = self.truncate_whitespaces(s)
        if s[0] != '{' or s[-1] != '}':
            raise Exception('ParseError: invalid json dict ' + s)

        content = s[1:-1]
        for token in self.get_tokens(content):
            try:
                k, v = self.get_tokens(token, ':')
            except:
                raise Exception('ParseError: invalid json dict ' + token)

            if not self.is_valid_key(k):
                raise Exception('ParseError: key is not a string ' + token)
            result[eval(k)] = self.get_object_from_string(v)

        return result

    def is_valid_key(self, s):
        l = len(s)
        if s[0] == "'" and s[l-1] == "'":
	        return True
        if s[0] == "\"" and s[l-1] == "\"":
	        return True
        if s.replace('.','',1).isdigit():
	        return True
        return False


if __name__ == '__main__':
    from minitest import *
    import json

    parser = JSONParser()

    json_datas = ["[   {    } , {  }  ]",
                 "[   {  \"test \": 1  } , {  }  ]",]

    with test(object.must_equal):
        for json_data in json_datas:
            result = parser.get_object_from_string(json_data)
            expected = json.loads(json_data)
            result.must_equal(expected)
