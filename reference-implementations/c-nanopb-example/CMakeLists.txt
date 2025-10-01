cmake_minimum_required(VERSION 3.10)
project(firstmile_nanopb_example)

set(CMAKE_C_STANDARD 99)

include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}/nanopb
    ${CMAKE_CURRENT_SOURCE_DIR}/schema
)

set(NANOPB_SOURCES
    nanopb/pb_common.c
    nanopb/pb_encode.c
)

set(SCHEMA_SOURCES
    schema/firstmile.pb.c
    schema/google/protobuf/empty.pb.c
    schema/google/protobuf/timestamp.pb.c
)

add_executable(firstmile_demo
    main.c
    ${NANOPB_SOURCES}
    ${SCHEMA_SOURCES}
)

target_compile_options(firstmile_demo PRIVATE -Wall -Wextra)