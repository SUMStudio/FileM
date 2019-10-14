from util.SingletonConfigEditor import SingletonConfigEditor


class delete_label:
    def execute(self, script_variable):
        print("label test")
        label_name = script_variable["cur_path"]
        file_name = script_variable["file_list"][0]
        i_dict = SingletonConfigEditor.instance().init_dict("global", "labels")
        i_dict[label_name].remove(file_name)
        # for i in i_dict:
        #     if file in i_dict[i]:
        #         i_dict[i].remove(file)
        SingletonConfigEditor.instance().dict_add("global", "labels", i_dict)

