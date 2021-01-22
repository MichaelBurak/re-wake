import streamlit as st
import gpt_2_simple as gpt2
import tensorflow as tf


sess = gpt2.start_tf_sess(threads=1)
gpt2.load_gpt2(sess)

generate_count = 0


@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def text_gen(starting_text):
    global generate_count
    global sess
    gpt2.generate(sess,
                  length=int(250),
                  temperature=float(0.8),
                  top_k=int(0),
                  top_p=float(0),
                  prefix=starting_text,
                  include_prefix=True,
                  return_as_list=True)[0]

    generate_count += 1
    if generate_count == 8:
        # Reload model to prevent Graph/Session from going OOM
        tf.reset_default_graph()
        sess.close()
        sess = gpt2.start_tf_sess(threads=1)
        gpt2.load_gpt2(sess)
        generate_count = 0

        gc.collect()


if __name__ == '__main__':
    st.title('A Lot Of Fun (With GPT-2) At Finnegans Wake!')
    starting_text = st.text_area(
        'From riverrun to...')
    if starting_text:
        response = text_gen(starting_text)
