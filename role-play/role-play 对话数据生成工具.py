from zhipuai import ZhipuAI

def create_role(key, novel_fragment):
    client = ZhipuAI(api_key=key)
    response = client.chat.completions.create(
        model="glm-4",
        messages=[
            {"role": "system", "content": "你是一个乐于解答各种问题的助手，你的任务是为用户提供专业、准确、有见地的建议。"},
            {"role": "user", "content": "根据小说片段,生成两个角色人设.\n\n按以下格式返回:\n角色名称\n角色描述\n\n 小说片段:%s " % novel_fragment}
        ],
    )
    content = response.choices[0].message.content
    role_texts = content.split("角色名称")
    roles = []
    for role_text in role_texts:
        if role_text == "":
            continue

        role = role_text.split("角色描述")
        roles.append({
            "name": role[0].replace("\n","").replace("：",""),
            "description": role[1].replace("\n","").replace("：","")
        })
    return roles

def talk(key, roles, turn):
    role1 = roles[0]
    role1_contents = []
    role2 = roles[1]
    role2_contents = []

    # role1 说第一句话
    role1_contents.append("妈妈...\n")

    # 对话轮次
    i = 0
    while i < turn:
        # role2 对 role1 说
        content2 = talk_to_glm(key, user_role=role1, user_contents=role1_contents, bot_role=role2, bot_contents=role2_contents)
        role2_contents.append(content2)

        # role1 对 role2 说
        content1 = talk_to_glm(key, user_role=role2, user_contents=role2_contents, bot_role=role1, bot_contents=role1_contents)
        role1_contents.append(content1)

        i += 1

    return to_conversation(role1, role1_contents, role2, role2_contents)

def to_conversation(role1, role1_contents, role2, role2_contents):
    conversations = []
    name1 = role1["name"]
    name2 = role2["name"]
    len1 = len(role1_contents)
    len2 = len(role2_contents)
    for i in range(0, max(len1, len2)):
        if i < len1:
            content1 = role1_contents[i]
            conversations.append({
                "name": name1,
                "content": content1
            })
        if i < len2:
            content2 = role2_contents[i]
            conversations.append({
                "name": name2,
                "content": content2
            })
    return conversations

def talk_to_glm(key, user_role, user_contents, bot_role, bot_contents):
    client = ZhipuAI(api_key=key)

    messages = []
    for i in range(0, len(user_contents)):
        messages.append({
            "role": "user",
            "content": user_contents[i]
        })
        if i < len(bot_contents):
            bot_content = bot_contents[i]
            messages.append({
                "role": "assistant",
                "content": bot_content
            })

    response = client.chat.completions.create(
        model="charglm-3",
        meta={
            "user_name": user_role['name'],
            "user_info": user_role['description'],
            "bot_name": bot_role['name'],
            "bot_info": bot_role['description']
        },
        messages=messages
    )
    content = response.choices[0].message.content
    return content

if __name__ == '__main__':
    key = ""

    with open("role-play/角色背景.txt", "r") as file:
        roles = create_role(key, file.read())

    conversations = talk(key, roles, 3)

    with open("role-play/对话.txt", "w") as file:
        for conversation in conversations:
            file.write("%s:%s" %(conversation["name"], conversation["content"]))
